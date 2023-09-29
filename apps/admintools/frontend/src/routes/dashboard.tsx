import { DashboardGroup } from '@/components/ui/dashboard_group';
import { useApp } from '@/contexts/app';
import { isParentPath } from '@/routes';

export default function DashboardRoute() {
    const { paths } = useApp();

    return (
        <div className="grid grid-cols-4">
            {paths.map(
                (path) =>
                    isParentPath(path) &&
                    path.show_in_menu && (
                        <DashboardGroup
                            label={path.label}
                            icon={path.icon}
                            key={path.label}
                        >
                            {path.children.map(
                                (child) =>
                                    child.show_in_menu && (
                                        <DashboardGroup.Item
                                            to={child.url}
                                            icon={child.icon}
                                            key={child.label}
                                        >
                                            {child.label}
                                        </DashboardGroup.Item>
                                    ),
                            )}
                        </DashboardGroup>
                    ),
            )}
        </div>
    );
}
