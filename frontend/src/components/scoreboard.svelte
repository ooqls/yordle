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


<script>
  import List, { Item, Separator, Text } from '@smui/list'; 
  import Score from "./score.svelte";
  export let scores = {}
  export let currentPlayerId = ""
  let rank = 0
  $: scores, rank = calculateRank()

  function calculateRank() {
    let sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1])
    let rank = sortedScores.findIndex(([key, value]) => key === currentPlayerId) + 1
    return rank
  }
</script>