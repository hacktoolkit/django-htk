import { Loader2Icon } from 'lucide-react';

export function HeaderLeftSide() {
    return (
        <div className="ltr:mr-2 rtl:ml-2 hidden sm:block">
            <Loader2Icon
                strokeWidth={1}
                className="global-loading-icon animate-spin opacity-0"
            />
        </div>
    );
}
