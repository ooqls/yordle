

<!-- <svelte:window  on:resize={() => { updateTitle(window) } } /> -->
<body>
  <div class="game-menu">
    <!-- <h1>{ title }</h1> -->
    <Title title="GAMES"></Title>
    {#if availableGames.length === 0 || loading }
    <div>  
      <CircularProgress style="height: 32px; width: 32px;" indeterminate />
    </div>
    {:else}
    
    <div class="game-list">
      {#each liveGames as game}
      <Card>
        <Content>{ game.key }</Content>
        <Actions>
          <Button href="/{game.name}/{game.key}">
            <Label>Join</Label>
          </Button>
        </Actions>
      </Card>
      {/each}

      {#each availableGames as game}
      <Card>
        <Content>{ game }</Content>
        <Actions>
          <Button on:click={() => { startNewGame(game) } }>
            <Label>Play</Label>
          </Button>
        </Actions>
      </Card>
      {/each}

      {#each loadingGames as game}
      <Card>
        <Content>Startng { game }...</Content>
      </Card>
      {/each}
    </div>
    {/if}
  </div>

  <style>
    .game-menu {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 20px;
    }
    .game-list {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 20px;
    }

    .game-list .mdc-card {
      flex: auto;
    }

    
  </style>
</body>

<script>
  import { onDestroy, onMount } from "svelte";
  import Title from "$components/title.svelte";
  import { games } from 'stores/games';
  import { goto } from "$app/navigation";

  import Card, {
    Content,
    PrimaryAction,
    Actions,
    ActionButtons,
    ActionIcons,
  } from '@smui/card';
  import Button, { Label } from '@smui/button';
  import CircularProgress from '@smui/circular-progress';
  import { api } from 'stores/url';

  export let data;


  /**
   * @type {string[]}
   */
  let availableGames = [];

  /**
   * @type {string[]}
  */
  let loadingGames = [];

  let loading = true;

  /**
   * @typedef {Object} LiveGame
   * @property {string} name
   * @property {string} key
   */

  /**
   * @type {LiveGame[]} liveGames
   */
  let liveGames = [];

  /**
   * @type {Function}
   */
  let unsubscribe;

  let apiURL = api();

  /**
   * @typedef {Object} GameList
   * @property {string[]} game_list
   * @property {LiveGame[]} active_games
   */

  /**
   * @param {GameList} value
   */
  function updateGames(value) {
    availableGames = value.game_list || [];
    liveGames = value.active_games || [];
  }

  onMount(() => {
    unsubscribe = games.subscribe(updateGames);
    console.log('mounted');


    setTimeout(() => {
      loading = false;
    }, 1000);

  });

  onDestroy(() => {
    console.log('unmounted');
    if (unsubscribe) {
      unsubscribe();
    }
  });


  /**
   * starts a new game
   * @param {String} game
   */
  async function startNewGame(game) {
    let resp = await fetch(`/api/${game}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "clientid": data.clientId,
      },
      body: game,
    });

    if (resp.ok && resp.body != undefined) {
      const newGame = await resp.json();
      console.log(`going to ${newGame.game_key}`)
      // go to page with key
      
      goto(`/${game}/${newGame.game_key}`);
    }
    
  }

  /**
   * 
   * @param {string} letter
   */
  function addLetter(letter) {
      answer += letter;
  }

  function removeLetter() {
      answer = answer.slice(0, -1);
  }
</script>
