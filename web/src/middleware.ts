import {
    type NextRequest,
    type MiddlewareConfig,
    type NextFetchEvent,
    NextResponse,
} from "next/server";
import { type NextRequestWithAuth, withAuth } from "next-auth/middleware";

export async function middleware(req: NextRequest, ev: NextFetchEvent) {
    if (req.nextUrl.pathname === "/") {
        return NextResponse.next();
    }

    const nextAuthMiddlware = withAuth({});
    const response = await nextAuthMiddlware(req as NextRequestWithAuth, ev);
    return response;
}

export const config: MiddlewareConfig = {
    matcher: [
        "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|auth).*)",
    ],
};
