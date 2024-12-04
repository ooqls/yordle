<!-- <div class="board-container">
  {#each Object.entries(scores) as [key, value]}
    <div class="score-entry">
      {#if key === currentPlayerId}
      <Score score={value} player={"you"} />
      {:else}
      <Score score={value} player={key} />
      {/if}
    </div>
  {/each}
</div> -->
<List>
  {#each Object.entries(scores) as [key, value]}
  <Item class={key === currentPlayerId ? 'activated' : ''}>
    <Text>
      <Score score={value} player={key === currentPlayerId ? "you" : key} />
    </Text>
  </Item>
  <Separator />
  {/each}
</List>

<style>
  .board-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 8px;
    padding: 16px;
    max-width: 400px;
    margin: 0 auto;
    border: 2px solid var(--mdc-theme-primary);
  }

  .score-entry {
    display: flex;
    justify-content: space-between;
    width: 100%;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 8px 16px;
    margin: 8px 0;
    transition: transform 0.2s;
  }

  .score-entry:hover {
    transform: scale(1.02);
  }
</style>

<script>
  import List, { Item, Separator, Text } from '@smui/list'; 
  import Score from "./score.svelte";
  export let scores = {}
  export let currentPlayerId = ""
</script>