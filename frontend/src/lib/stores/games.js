import { readable, writable } from 'svelte/store';


/**
 * This store will fetch the games from the API every second.
 * 
 */
const games = readable([], (set, update) => {
  const interval = setInterval(() => {
    fetch("/api/games", {headers: {
      "accept": "application/json"
    }}).then(response => response.json()).then(data => {
      set(data)
    }).catch(error => {
      console.error('Error:', error);
    });
  }, 1000);

	return () => clearInterval(interval);
});

const activeGames = writable([], (set, update) => {
  const interval = setInterval(() => {
    fetch("/api/active", {headers: {
      "accept": "application/json"
    }}).then(response => response.json()).then(data => {
      set(data)
    }).catch(error => {
      console.error('Error:', error);
    });
  }, 1000);

  return () => clearInterval(interval);
})



export { games, activeGames }