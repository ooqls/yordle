export function load({ cookies  }) {

  let clientId = cookies.get("client-id")
  if (!clientId) {
    clientId = Math.random().toString(36).substring(7);
    cookies.set("client-id", clientId, { path: "/" });
  }
  console.log("client-id", clientId)

  return {
    clientId: clientId
  }
}