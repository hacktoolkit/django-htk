import React from 'react';
import { NavLink } from 'react-router-dom';

import { Icon, IconName } from '@/components/ui/icon';

export function NavItem({
    to,
    icon,
    children,
    anchor = false,
}: {
    to: string;
    icon: IconName;
    children: React.ReactNode;
    anchor?: boolean;
}) {
    const linkContent = (
        <div className="flex items-center">
            <Icon name={icon} className="shrink-0 group-hover:!text-primary" />
            <span className="text-black ltr:pl-3 rtl:pr-3 dark:text-[#506690] dark:group-hover:text-white-dark">
                {children}
            </span>
        </div>
    );
    return (
        <li className="nav-item">
            {anchor ? (
                <a href={to} className="group">
                    {linkContent}
                </a>
            ) : (
                <NavLink to={to} className="group">
                    {linkContent}
                </NavLink>
            )}
        </li>
    );
}
