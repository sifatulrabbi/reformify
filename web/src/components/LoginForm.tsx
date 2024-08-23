"use client";
import { type SyntheticEvent, useEffect, useState } from "react";
import { BsKeyFill, BsEnvelopeFill } from "react-icons/bs";
import { signIn } from "next-auth/react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { FaGithub } from "react-icons/fa";

export default function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const { data: session, status } = useSession();

    useEffect(() => {
        setLoading(status === "loading");
    }, [status]);

    async function login(e: SyntheticEvent<HTMLFormElement>) {
        e.preventDefault();
        setLoading(true);
        const res = await signIn("credentials", { email, password });
        if (res?.error) {
            setLoading(false);
        } else {
            console.log("login successful:", res);
        }
    }

    async function signInWithGithub() {
        await signIn("github");
    }

    if (loading)
        return (
            <div className="w-full flex flex-col gap-6 p-6 max-w-[90%] md:max-w-xl items-center">
                <div className="dui-loading dui-loading-infinity dui-loading-lg"></div>
                Please wait...
            </div>
        );

    return (
        <div className="w-full flex flex-col gap-6 p-6 max-w-[90%] md:max-w-xl items-center">
            {status === "authenticated" && session && session.user && (
                <Link
                    href="/profile"
                    className="dui-btn dui-btn-primary font-normal"
                >
                    Continue as{" "}
                    <span className="font-bold">
                        {session.user.name || session.user.email}
                    </span>
                </Link>
            )}
            <form
                action="submit"
                onSubmit={login}
                className="w-full flex flex-col gap-6"
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
            <div className="text-md">
                Don&apos;t have an account?{" "}
                <Link href="/register" className="dui-link dui-link-primary">
                    Register
                </Link>
            </div>
            <div className="w-full flex flex-row items-center gap-4">
                <hr className="w-full border-gray-700" />
                Or
                <hr className="w-full border-gray-700" />
            </div>
            <button
                onClick={signInWithGithub}
                type="button"
                className="dui-btn w-full"
            >
                <FaGithub />
                GitHub
            </button>
        </div>
    );
}
