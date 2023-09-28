export type ThemeConfig = {
    // Locale
    locale: 'en';
    theme: 'light' | 'dark' | 'system';
    sidebarWidth: number; // in pixel
    isSidebarOpen: boolean;
    menu: 'vertical' | 'collapsible-vertical' | 'horizontal';
    layout: 'full' | 'boxed-layout';
    rtlClass: 'ltr' | 'rtl';
    navbar: 'navbar-sticky' | 'navbar-floating' | 'navbar-static';
    semiDark: boolean; // Navbar and header section becomes dark
    // Page change animation
    animation:
        | ''
        | 'animate__fadeIn'
        | 'animate__fadeInDown'
        | 'animate_fadeInUp'
        | 'animate__fadeInLeft'
        | 'animate__fadeInRight'
        | 'animate__slideInDown'
        | 'animate__slideInLeft'
        | 'animate__slideInRight'
        | 'animate__zoomIn';
};

export const defaultThemeConfig: ThemeConfig = {
    locale: 'en',
    theme: 'light',
    sidebarWidth: 260,
    isSidebarOpen: true,
    menu: 'vertical',
    layout: 'full',
    rtlClass: 'ltr',
    animation: '',
    navbar: 'navbar-sticky',
    semiDark: false,
};
