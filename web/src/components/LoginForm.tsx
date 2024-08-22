"use client";
import { type SyntheticEvent, useState } from "react";
import { BsKeyFill, BsEnvelopeFill } from "react-icons/bs";
import { signIn } from "next-auth/react";

export default function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    async function login(e: SyntheticEvent<HTMLFormElement>) {
        e.preventDefault();
        setLoading(true);
        const res = await signIn("credentials", {
            email,
            password,
            redirect: false,
        });
        if (res?.error) {
            setLoading(false);
        } else {
            console.log("login successful:", res);
        }
    }

    return (
        <form
            action="submit"
            onSubmit={login}
            className="w-full flex flex-col gap-6 p-6 max-w-[90%] md:max-w-xl"
        >
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsEnvelopeFill />
                <input
                    value={password}
                    onChange={(e) => setPassword(e.currentTarget.value)}
                    type="text"
                    className="grow"
                    placeholder="Email"
                    required
                />
            </label>
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsKeyFill />
                <input
                    value={email}
                    onChange={(e) => setEmail(e.currentTarget.value)}
                    type="password"
                    className="grow"
                    placeholder="Password"
                    required
                />
            </label>
            <button type="submit" className="dui-btn dui-btn-primary">
                Login
            </button>
        </form>
    );
}
