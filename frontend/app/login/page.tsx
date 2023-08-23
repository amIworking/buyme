
import Link from "next/link";
import "./style.css"

const Login = () => {

    return (
        <main className="login">
            <h1 className="login__title">Авторизация</h1>
            <form className="login__form">
                <input type="text" placeholder="имя пользователя" className="login__input" />
                <input type="password" placeholder="пароль" className="login__input" />
                <button type="submit" className="login__submit-btn">Войти</button>
            </form>
            <div className="login__registr-wrapper">
                <Link href="/registration" className="login__regist-link">
                    Регистрация
                </Link>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    shapeRendering="geometricPrecision"
                    textRendering="geometricPrecision"
                    imageRendering="optimizeQuality"
                    fillRule="evenodd"
                    clipRule="evenodd"
                    viewBox="0 0 512 243.58"
                    className="login__registr-icon"
                >
                    <path
                        fillRule="nonzero"
                        d="M373.57 0 512 120.75 371.53 243.58l-20.92-23.91 94.93-83L0 137.09v-31.75l445.55-.41-92.89-81.02z"
                    />
                </svg>
            </div>

        </main>
    );
}

export default Login;