import { readable, writable } from 'svelte/store';
import {GameList} from '$models/models.js'

/**
 * @type {GameList}
 */

/**
 *This store will fetch the games from the API every second.
 * @type {import('svelte/store').Readable<GameList> } games
 */
const games = readable(new GameList([], []), (set, update) => {
  const interval = setInterval(() => {
    fetch(`/api/games`, {headers: {
      "accept": "application/json"
    }}).then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch games")
      }
      return response.json()
    }).then(data => {
      set(data)
    })
  }, 1000);

	return () => clearInterval(interval);
});



export { games }