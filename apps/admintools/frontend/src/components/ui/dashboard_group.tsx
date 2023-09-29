import React from 'react';

import { Icon, IconName } from '@/components/ui/icon';
import { Link } from 'react-router-dom';

function Component({
    label,
    icon,
    children,
}: {
    label: string;
    icon: IconName;
    children: React.ReactNode;
}) {
    return (
        <div className="panel h-full">
            <h5 className="mb-5 text-lg font-semibold dark:text-white-light">
                <Icon name={icon}>{label}</Icon>
            </h5>
            <ul className="font-semibold">{children}</ul>
        </div>
    );
}

function Item({
    to,
    icon,
    children,
}: {
    to: string;
    icon: IconName;
    children: React.ReactNode;
}) {
    return (
        <li>
            <Link
                to={to}
                className="block rounded-md p-2 pb-1 hover:bg-white-dark/10 hover:text-primary"
            >
                <Icon name={icon} size="md">
                    {children}
                </Icon>
            </Link>
        </li>
    );
}

export const DashboardGroup = Object.assign(Component, { Item });
