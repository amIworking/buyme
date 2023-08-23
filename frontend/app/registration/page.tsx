"use client"
import Link from "next/link";
import "./style.css"
import { useState } from "react";

const Registration = () => {
    const [password, setPassword] = useState('')
    const [checkPass, setCheckPass] = useState('')
    const [passwordAlert, setPasswordAlert] = useState(false)
    return (
        <main className="registr">
            <h1 className="registr__title">Регистрация</h1>
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                }}
                className="registr__form">
                <input
                    required
                    type="text"
                    placeholder="имя пользователя"
                    className="registr__input"
                />
                <input
                    required
                    title="Пароль должен содержать от 8ми до 24х символов, включая заглвную букву и цифру"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    type="password"
                    placeholder="пароль"
                    className="registr__input"
                    onChange={(e) => {
                        setPassword(e.target.value)
                        if (e.target.value === checkPass) setPasswordAlert(false)

                    }}
                />
                <input
                    required
                    title="Пароль должен содержать от 8ми до 24х символов, включая заглвную букву и цифру"
                    type="password"
                    placeholder="повторите пароль"
                    className="registr__input"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    onChange={(e) => {
                        setCheckPass(e.target.value)
                        if (password === e.target.value) setPasswordAlert(false)

                    }}
                />
                <strong className={passwordAlert ? "registr__password-alert registr__password-alert--active" : "registr__password-alert"}>Пароли не совпадают!</strong>
                <button
                    type="submit"
                    className="registr__submit-btn"
                    onClick={(e) => {
                        e.preventDefault()
                        if (password !== checkPass) setPasswordAlert(true)
                    }}
                >Зарегистрироваться
                </button>
            </form>

            <div className="registr__registr-wrapper">
                <Link href="/login" className="registr__regist-link">
                    Есть аккаунт?
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

export default Registration;