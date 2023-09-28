import { useBoolean } from '@/hooks';
import React from 'react';

export function GoTopButton() {
    const [show, handleShow, handleHide] = useBoolean();

    const handleClick = () => {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };

    React.useEffect(() => {
        const handleScroll = () => {
            if (
                document.body.scrollTop > 50 ||
                document.documentElement.scrollTop > 50
            ) {
                handleShow();
            } else {
                handleHide();
            }
        };
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        show && (
            <div className="fixed bottom-6 ltr:right-6 rtl:left-6 z-50">
                <button
                    type="button"
                    className="btn btn-outline-primary rounded-full p-2 animate-pulse bg-[#fafafa] dark:bg-[#060818] dark:hover:bg-primary"
                    onClick={handleClick}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-4 w-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth="1.5"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M8 7l4-4m0 0l4 4m-4-4v18"
                        />
                    </svg>
                </button>
            </div>
        )
    );
}
