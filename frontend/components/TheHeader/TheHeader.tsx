"use client"
import { usePathname } from "next/navigation"
import Link from "next/link";
import "./style.css"

const TheHeader = () => {
    const pathname = usePathname()

    return (
        <header>
            <div className="container">
                <div className="header">
                    <Link href="/" className="header__logo">BUYME</Link>
                    <nav className="header__nav">
                        <Link href="/catalog" className={pathname === '/catalog' ? "header__nav-link header__nav-link--active" : "header__nav-link"}>Каталог</Link>
                        <Link href="/reviews" className={pathname === '/reviews' ? "header__nav-link header__nav-link--active" : "header__nav-link"}>Отзывы</Link>
                        <Link href="/about" className={pathname === '/about' ? "header__nav-link header__nav-link--active" : "header__nav-link"}>О нас</Link>

                    </nav>
                    <aside className="header__aside">
                        <Link
                            href="/login"
                            className={pathname === '/login' || pathname === '/registration' ? "header__aside-link login-btn login-btn--active" : "header__aside-link login-btn"}
                        >Вход
                        </Link>
                        <Link href="/bag" className="header__aside-link">
                            <svg
                                className="header__nav-bagicon"
                                version="1.1"
                                id="Layer_1"
                                xmlns="http://www.w3.org/2000/svg"
                                xmlnsXlink="http://www.w3.org/1999/xlink"
                                x="0px"
                                y="0px"
                                viewBox="0 0 122.88 94.27"
                                xmlSpace="preserve"
                            >
                                <style
                                    type="text/css"
                                    dangerouslySetInnerHTML={{
                                        __html: ".bag-icon{fill-rule:evenodd;clip-rule:evenodd;}"
                                    }}
                                />
                                <g>
                                    <path
                                        className="bag-icon"
                                        d="M12.04,27.72h9.43L44.56,1.86c2.05-2.3,5.61-2.5,7.9-0.45v0c2.3,2.05,2.5,5.61,0.45,7.91l-16.42,18.4h50.32 L70.39,9.32c-2.05-2.3-1.85-5.86,0.45-7.91h0c2.3-2.05,5.85-1.85,7.91,0.45l23.08,25.86l9.02,0l0.12,0l8.47,0 c1.9,0,3.45,1.55,3.45,3.45v9.73c0,1.9-1.55,3.45-3.45,3.45h-7.33l-3.77,47.53c-0.1,1.31-1.08,2.39-2.39,2.39H16.94 c-1.31,0-2.29-1.08-2.39-2.39l-3.77-47.53H3.45C1.55,44.35,0,42.8,0,40.9v-9.73c0-1.9,1.55-3.45,3.45-3.45l8.47,0L12.04,27.72 L12.04,27.72z M77.67,46.22h10.91v31.53l-10.91,0V46.22L77.67,46.22z M56.45,46.22h10.9v31.53l-10.9,0V46.22L56.45,46.22z M35.23,46.22h10.91v31.53l-10.91,0V46.22L35.23,46.22z"
                                    />
                                </g>
                            </svg>
                        </Link>
                    </aside>
                </div>
            </div>

        </header>
    );
}

export default TheHeader;