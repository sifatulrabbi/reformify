import {
    type NextRequest,
    NextResponse,
    type MiddlewareConfig,
} from "next/server";

export async function middleware(req: NextRequest) {
    console.log("middleware running");
    return NextResponse.next();
}

export const config: MiddlewareConfig = {
    matcher: [
        "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|auth).*)",
    ],
};
