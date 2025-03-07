import { mdiCookieSettings } from "@mdi/js";

export function load({ params, cookies }) {
  let clientId = cookies.get("client-id");
  if (!clientId) {
    clientId = Math.random().toString(36).substring(7);
    cookies.set("client-id", clientId, { path: "/", secure: true });
  }

  return {
    clientId: clientId,
    gameKey: params.key,
  };
}
