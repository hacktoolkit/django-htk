import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ActivitySquareIcon, HammerIcon, LogOutIcon } from 'lucide-react';

export function UserMenu() {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button
                    variant="ghost"
                    className="relative w-9 h-9 rounded-full saturate-50 hover:saturate-100 bg-white-light/40 dark:bg-dark/40 hover:text-primary dark:hover:bg-dark/60"
                >
                    <Avatar>
                        <AvatarImage src="/static/some-image.jpg" />
                        <AvatarFallback>U</AvatarFallback>
                    </Avatar>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
                className="w-56 bg-white dark:bg-dark"
                align="end"
            >
                <DropdownMenuLabel>User Menu</DropdownMenuLabel>
                <DropdownMenuGroup>
                    <DropdownMenuItem>
                        <ActivitySquareIcon className="mr-2 h-4 w-4" />
                        <span>Django Admin</span>
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                        <HammerIcon className="mr-2 h-4 w-4" />
                        <span>AdminTools</span>
                    </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                    <DropdownMenuItem>
                        <LogOutIcon className="mr-2 h-4 w-4" />
                        <span>Log Out</span>
                    </DropdownMenuItem>
                </DropdownMenuGroup>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
