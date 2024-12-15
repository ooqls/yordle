<div>
  <div class="game-menu">
    <!-- <h1>{ title }</h1> -->
    <Title title="GAMES"></Title>
    {#if availableGames.length === 0 || loading}
    <div>  
      <CircularProgress style="height: 32px; width: 32px" indeterminate/>
    </div>
    {:else}
    
    <div class="game-list">
      {#each availableGames as game}
      <Card>
        <PrimaryAction onclick={() => { startNewGame(game)}}> 

          <Content class="game-card"><b>{ game }</b></Content>
        <!-- <Actions>
          <Button onclick={() => { startNewGame(game) } }>
            <Label>Play</Label>
          </Button>
        </Actions> -->
        </PrimaryAction>
      </Card>
      {/each}

      {#each liveGames as game}
      <Card>
        <PrimaryAction onclick={() => goto(`${game.name}/${game.key}`)}> 
          <Content class="game-card">
            <p>
              <b>{ game.key }</b>
              <br />
              { game.name }
            </p>
          </Content>
        <!-- <Actions>
          <Button onclick={() => goto(`${game.name}/${game.key}`)}>
            <Label>Join</Label>
          </Button>
        </Actions> -->
        </PrimaryAction>
      </Card>
      {/each}
    </div>
    {/if}
  </div>
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

  * :global(.game-card) {
    min-width: 100px;
    min-height: 100px;
    justify-content: center;
    text-align: center;
    font-size: larger;
    display: flex;
    align-items: center;
  }


  
</style>

<script>
  import { onDestroy, onMount } from "svelte";
  import Title from "$components/title.svelte";
  import { games } from 'stores/games';
  import { goto } from "$app/navigation";

  import Card, {
    Content,
    PrimaryAction,
    Media,
    Actions,
    MediaContent,
  } from '@smui/card';
  import Ripple from "@smui/ripple";
  import Button, { Label } from '@smui/button';
  import CircularProgress from '@smui/circular-progress';

  let { data } = $props();


  /**
   * @type {string[]}
   */
  let availableGames = $state([]);



  let loading = $state(true);

  /**
   * @typedef {Object} LiveGame
   * @property {string} name
   * @property {string} key
   */

  /**
   * @type {LiveGame[]} liveGames
   */
  let liveGames = $state([]);

  /**
   * @type {Function}
   */
  let unsubscribe;


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


    setTimeout(() => {
      loading = false;
    }, 1000);

  });

  onDestroy(() => {
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
      // go to page with key
      
      goto(`/${game}/${newGame.game_key}`);
    }
    
  }
</script>
