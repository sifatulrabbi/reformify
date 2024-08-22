"use client";
import { BsKeyFill, BsEnvelopeFill, BsPersonFill } from "react-icons/bs";

export default function RegistrationForm() {
    return (
        <form
            action="submit"
            onSubmit={(e) => e.preventDefault()}
            className="w-full flex flex-col gap-6 p-6 max-w-[90%] md:max-w-xl"
        >
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsPersonFill />
                <input className="grow" placeholder="Full name" required />
            </label>
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsEnvelopeFill />
                <input
                    type="text"
                    className="grow"
                    placeholder="Email"
                    required
                />
            </label>
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsKeyFill />
                <input
                    type="password"
                    className="grow"
                    placeholder="Password"
                    required
                />
            </label>
            <label className="dui-input dui-input-bordered flex items-center gap-2">
                <BsKeyFill />
                <input
                    type="password"
                    className="grow"
                    placeholder="Re-enter password"
                    required
                />
            </label>
            <button type="submit" className="dui-btn dui-btn-primary">
                Register
            </button>
        </form>
    );
}
