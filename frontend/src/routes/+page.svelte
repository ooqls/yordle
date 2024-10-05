

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
          <Button href="/yordle/{game.key}">
            <Label>Join</Label>
          </Button>
        </Actions>
      </Card>
      {/each}

      {#each availableGames as game}
      <Card>
        <Content>{ game }</Content>
        <Actions>
          <Button on:click={() => { startNewGame(game)}}>
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
  import { onMount } from "svelte";
  import Title from "../components/title.svelte";
  import { games, activeGames } from 'stores/games';
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

    import { redirect } from "@sveltejs/kit";
  let answer = 'hello';

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


  onMount(() => {
    games.subscribe(value => {
      availableGames = value
    });

    activeGames.subscribe(value => {
      liveGames = value
    });
    console.log('mounted');

    setTimeout(() => {
      loading = false;
    }, 1000);
  });


  /**
   * starts a new game
   * @param {String} game
   */
  async function startNewGame(game) {
    let resp = await fetch(`/api/games?game=${game}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: game,
    });

    if (resp.ok && resp.body != undefined) {
      const newGame = await resp.json();
      console.log(`going to ${newGame.game}`)
      // go to page with key
      goto(`/yordle/${newGame.game_key}`)
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
