import { mdiCookieSettings } from '@mdi/js';

export function load({params, cookies}) {
  return {
    game_key: params.game,
    clientId: cookies.get("client-id"),
  }
}