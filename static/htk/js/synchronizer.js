const HtkSynchronizer = function(cfg) {
    this.url = cfg.url || window.location;
    this.saveSuccessCallback = cfg.saveSuccessCallback || null;
    this.saveErrorCallback = cfg.saveErrorCallback || null;

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = $.cookie('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    this.state = {
        isSaving : false,
        hasSaved : false,
        pendingSaveOperation : null,
        formData : {}
    };

    this.setState = function(newState) {
        _.forIn(newState, function(value, key) {
            this.state.key = value;
        }, this);
    };

    this.updateValues = function(opts, eventType) {
        var formData = this.state.formData;
        var newState = {};
        _.forIn(opts, function(value, key) {
            formData[key] = value;
        });
        newState.formData = formData;
        this.setState(newState);
        this.queueSave(eventType);
    };

    this.cancelSave = function() {
        if (this.state.pendingSaveOperation) {
            clearTimeout(this.state.pendingSaveOperation);
            this.setState({
                pendingSaveOperation: null
            });
        }
    };

    this.queueSave = function(eventType) {
        var delayMap = {
            'change' : 2500,
            'blur' : 1000
        };
        var delay = delayMap[eventType] || 1000;
        //console.log('save queued for ' + delay);
        var _this = this;
        this.cancelSave();
        var pendingSaveOperation = setTimeout(function() {
            _this.doSave();
        }, delay);
        this.setState({
            pendingSaveOperation: pendingSaveOperation
        });
    };

    this.onSaveSuccess = function(data) {
        this.clearUpdatedDataFromSave(data);
        this.setState({
            saveSuccess : true
        })
        if (this.saveSuccessCallback) {
            this.saveSuccessCallback(data);
        }
    };

    this.onSaveError = function() {
        this.setState({
            saveSuccess : false
        });
        if (this.saveErrorCallback) {
            this.saveErrorCallback();
        }
    };

    this.onSaveEnd = function(data) {
        this.setState({
            isSaving : false,
            hasSaved : true
        });
    };

    this.clearUpdatedDataFromSave = function(data) {
        var formData = this.state.formData;
        _.forIn(data, function(value, key) {
            if (formData[key] === value) {
                // delete pending save data that matches already persisted key-value
                delete formData[key];
            }
        });
        this.setState({
            formData: formData
        });
    };

    this.doSave = function() {
        if (this.state.disabled) {
            return false;
        }
        var formData = this.state.formData;

        this.setState({
            isSaving : true
        });
        var _this = this;

        $.ajax(
            this.url,
            {
                method: 'POST',
                data: formData
            }
        ).done(function(data) {
            _this.onSaveSuccess(data);
        }).fail(function() {
            _this.onSaveError();
        }).always(function(data) {
            _this.onSaveEnd(data);
        });
    };
};
