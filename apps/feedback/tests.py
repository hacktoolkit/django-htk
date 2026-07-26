# Python Standard Library Imports
import json
from unittest import mock

# Django Imports
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.db import connection
from django.test import RequestFactory
from django.test import TestCase
from django.test import override_settings

# HTK Imports
from htk.api.constants import HTK_API_KEY_ANTISPAM
from htk.api.constants import HTK_API_VALUE_ANTISPAM_CHALLENGE_RESPONSE
from htk.apps.accounts.utils.general import get_user_profile_model
from htk.apps.feedback.constants import FEEDBACK_REQUEST_TYPE_BUG
from htk.apps.feedback.constants import FEEDBACK_REQUEST_TYPE_FEATURE
from htk.apps.feedback.constants import FEEDBACK_STATUS_IN_PROGRESS
from htk.apps.feedback.constants import FEEDBACK_VISIBILITY_PRIVATE
from htk.apps.feedback.constants import FEEDBACK_VISIBILITY_PUBLIC
from htk.apps.feedback.constants import FEEDBACK_VOTE_DOWN
from htk.apps.feedback.constants import FEEDBACK_VOTE_UP
from htk.apps.feedback.models import Feedback
from htk.apps.feedback.models import FeedbackRequest
from htk.apps.feedback.models import FeedbackRequestComment
from htk.apps.feedback.models import FeedbackRequestVote
from htk.apps.feedback import views
from htk.utils.urls import build_full_url


@override_settings(SITE_ID=1)
class FeedbackRequestApiTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        self.factory = RequestFactory()
        self.site, _ = Site.objects.update_or_create(
            id=1,
            defaults={
                'domain': 'testserver',
                'name': 'testserver',
            },
        )
        User = get_user_model()
        self.user = User.objects.create_user(
            username='feedback-user',
            email='feedback-user@example.com',
            password='password',
            first_name='Feedback',
            last_name='Reader',
        )
        self.staff_user = User.objects.create_user(
            username='staff-user',
            email='staff-user@example.com',
            password='password',
            is_staff=True,
        )
        UserProfileModel = get_user_profile_model()
        UserProfileModel.objects.get_or_create(
            user=self.user,
            defaults={
                'has_username_set': True,
            },
        )
        UserProfileModel.objects.get_or_create(
            user=self.staff_user,
            defaults={
                'has_username_set': True,
            },
        )

    def _json(self, response):
        return json.loads(response.content.decode('utf-8'))

    def _request(self, method, path='/', data=None, user=None, **extra):
        data = {} if data is None else data
        if method == 'get':
            request = self.factory.get(path, data=data, **extra)
        else:
            request = self.factory.post(path, data=data, **extra)
        request.user = user if user is not None else AnonymousUser()
        return request

    @override_settings(
        HTK_FEEDBACK_SLACK_ENABLED=True,
        HTK_FEEDBACK_SLACK_CHANNEL='#feedback',
    )
    @mock.patch('htk.apps.feedback.services.slack_webhook_call')
    def test_request_submit_creates_request_vote_and_slack_notification(self, slack_webhook_call):
        request = self._request(
            'post',
            '/feedback/requests/submit',
            user=self.user,
            data={
                'title': 'Add reading plan support',
                'description': 'I want a plan for reading through Romans.',
                'type': FEEDBACK_REQUEST_TYPE_FEATURE,
                'context': json.dumps(
                    {
                        'route': 'reader',
                        'reference': 'Romans 8',
                    }
                ),
                'source_uri': '/bible/Romans/8',
            },
        )
        response = views.request_submit(request)
        payload = self._json(response)

        self.assertTrue(payload['success'])
        feedback_request = FeedbackRequest.objects.get()
        self.assertEqual('Add reading plan support', feedback_request.title)
        self.assertEqual({'route': 'reader', 'reference': 'Romans 8'}, feedback_request.context)
        self.assertEqual(self.user, feedback_request.created_by)
        self.assertEqual(FEEDBACK_VISIBILITY_PRIVATE, feedback_request.visibility)
        self.assertTrue(feedback_request.needs_review)
        self.assertEqual(1, feedback_request.votes_count)
        self.assertEqual(1, feedback_request.upvotes_count)
        self.assertEqual(0, feedback_request.downvotes_count)
        expected_full_admin_url = build_full_url(feedback_request.admin_url)
        self.assertEqual(
            expected_full_admin_url,
            feedback_request.full_admin_url,
        )
        vote = FeedbackRequestVote.objects.get()
        self.assertEqual(self.user, vote.user)
        self.assertEqual(FEEDBACK_VOTE_UP, vote.value)
        slack_webhook_call.assert_called_once()
        _, kwargs = slack_webhook_call.call_args
        self.assertEqual('#feedback', kwargs['channel'])
        self.assertEqual(':memo: New feedback submitted', kwargs['text'])
        attachment = kwargs['attachments'][0]
        self.assertEqual('Add reading plan support', attachment['title'])
        self.assertIn('Open in Django admin', attachment['fields'][-1]['value'])
        self.assertIn(expected_full_admin_url, attachment['fields'][-1]['value'])

    def test_request_submit_allows_anonymous_feedback_without_identity(self):
        request = self._request(
            'post',
            '/feedback/requests/submit',
            data={
                'title': 'Anonymous idea',
                'description': 'Contact fields should not be required.',
            },
        )
        response = views.request_submit(request)
        payload = self._json(response)
        feedback_request = FeedbackRequest.objects.get()

        self.assertTrue(payload['success'])
        self.assertIsNone(feedback_request.created_by)
        self.assertEqual(0, FeedbackRequestVote.objects.count())

    def test_request_list_searches_and_excludes_private_items_for_public_users(self):
        public_request = FeedbackRequest.objects.create(
            site=self.site,
            title='Improve Bible search',
            description='Support exact phrase searching.',
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
        )
        default_private_request = FeedbackRequest.objects.create(
            site=self.site,
            title='Search default private note',
        )
        FeedbackRequest.objects.create(
            site=self.site,
            title='Private admin note',
            visibility=FEEDBACK_VISIBILITY_PRIVATE,
        )

        request = self._request('get', '/feedback/requests', data={'q': 'search'})
        response = views.request_list(request)
        payload = self._json(response)

        self.assertTrue(payload['success'])
        self.assertEqual(FEEDBACK_VISIBILITY_PRIVATE, default_private_request.visibility)
        self.assertTrue(default_private_request.needs_review)
        self.assertEqual([public_request.id], [item['id'] for item in payload['requests']])

    def test_request_submit_non_staff_cannot_self_publish(self):
        request = self._request(
            'post',
            '/feedback/requests/submit',
            user=self.user,
            data={
                'title': 'Publish me immediately',
                'description': 'This should still need review.',
                'visibility': FEEDBACK_VISIBILITY_PUBLIC,
                'needs_review': 'false',
            },
        )
        response = views.request_submit(request)
        payload = self._json(response)
        feedback_request = FeedbackRequest.objects.get()

        self.assertTrue(payload['success'])
        self.assertEqual(FEEDBACK_VISIBILITY_PRIVATE, feedback_request.visibility)
        self.assertTrue(feedback_request.needs_review)

    def test_request_submit_staff_can_publish_reviewed_request(self):
        request = self._request(
            'post',
            '/feedback/requests/submit',
            user=self.staff_user,
            data={
                'title': 'Reviewed public request',
                'description': 'Staff can intentionally publish reviewed requests.',
                'visibility': FEEDBACK_VISIBILITY_PUBLIC,
                'needs_review': 'false',
            },
        )
        response = views.request_submit(request)
        payload = self._json(response)
        feedback_request = FeedbackRequest.objects.get()

        self.assertTrue(payload['success'])
        self.assertEqual(FEEDBACK_VISIBILITY_PUBLIC, feedback_request.visibility)
        self.assertFalse(feedback_request.needs_review)

    def test_duplicate_votes_update_existing_vote_direction_instead_of_incrementing(self):
        feedback_request = FeedbackRequest.objects.create(
            site=self.site,
            title='Add cross references',
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
        )
        first = self._request(
            'post',
            '/feedback/requests/%s/vote' % feedback_request.id,
            user=self.user,
            data={'direction': 'up'},
        )
        second = self._request(
            'post',
            '/feedback/requests/%s/vote' % feedback_request.id,
            user=self.user,
            data={'direction': 'down'},
        )

        self.assertTrue(self._json(views.request_vote(first, feedback_request.id))['success'])
        self.assertTrue(self._json(views.request_vote(second, feedback_request.id))['success'])
        feedback_request.refresh_from_db()
        vote = FeedbackRequestVote.objects.get()

        self.assertEqual(-1, feedback_request.votes_count)
        self.assertEqual(0, feedback_request.upvotes_count)
        self.assertEqual(1, feedback_request.downvotes_count)
        self.assertEqual(FEEDBACK_VOTE_DOWN, vote.value)

    def test_unvote_deactivates_vote_and_updates_count(self):
        feedback_request = FeedbackRequest.objects.create(
            site=self.site,
            title='Add Psalms reading mode',
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
        )
        feedback_request.vote(user=self.user)
        feedback_request.refresh_from_db()
        self.assertEqual(1, feedback_request.votes_count)
        self.assertEqual(1, feedback_request.upvotes_count)
        self.assertEqual(0, feedback_request.downvotes_count)

        request = self._request(
            'post',
            '/feedback/requests/%s/unvote' % feedback_request.id,
            user=self.user,
        )
        response = views.request_unvote(request, feedback_request.id)
        payload = self._json(response)
        feedback_request.refresh_from_db()

        self.assertTrue(payload['success'])
        self.assertEqual(1, payload['removed'])
        self.assertEqual(0, feedback_request.votes_count)
        self.assertEqual(0, feedback_request.upvotes_count)
        self.assertEqual(0, feedback_request.downvotes_count)

    def test_comment_and_staff_status_update(self):
        feedback_request = FeedbackRequest.objects.create(
            site=self.site,
            title='Report typo in John',
            request_type=FEEDBACK_REQUEST_TYPE_BUG,
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
        )
        comment_request = self._request(
            'post',
            '/feedback/requests/%s/comment' % feedback_request.id,
            user=self.user,
            data={'comment': 'This happens on John 3:16.'},
        )
        status_request = self._request(
            'post',
            '/feedback/requests/%s/status' % feedback_request.id,
            user=self.staff_user,
            data={
                'status': FEEDBACK_STATUS_IN_PROGRESS,
                'message': 'We are checking the content import.',
            },
        )

        self.assertTrue(self._json(views.request_comment(comment_request, feedback_request.id))['success'])
        self.assertTrue(self._json(views.request_status_update(status_request, feedback_request.id))['success'])
        feedback_request.refresh_from_db()

        self.assertEqual(1, FeedbackRequestComment.objects.count())
        self.assertEqual(FEEDBACK_STATUS_IN_PROGRESS, feedback_request.status)

    @mock.patch('htk.apps.feedback.forms.feedback_email')
    def test_legacy_submit_endpoint_still_creates_feedback(self, feedback_email):
        if Feedback._meta.db_table not in connection.introspection.table_names():
            self.skipTest('Legacy htk.Feedback table is not installed in this test project')
        request = self._request(
            'post',
            '/feedback/submit',
            data={
                HTK_API_KEY_ANTISPAM: HTK_API_VALUE_ANTISPAM_CHALLENGE_RESPONSE,
                'name': 'Legacy User',
                'email': 'legacy@example.com',
                'comment': 'Old form still works.',
            },
            HTTP_REFERER='/old/page',
        )
        request.user = self.user
        response = views.submit(request)
        payload = self._json(response)

        self.assertTrue(payload['success'])
        self.assertEqual(1, Feedback.objects.count())
        self.assertEqual('/old/page', Feedback.objects.get().uri)
        feedback_email.assert_called_once()
