import { readable, writable } from 'svelte/store';
import  { api } from './url.js'


/**
 * This store will fetch the games from the API every second.
 */
const games = readable([], (set, update) => {
  const interval = setInterval(() => {
    let apiURL = api()
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