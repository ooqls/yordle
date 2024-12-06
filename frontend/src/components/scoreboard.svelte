<div class={disableMobileView ? "always-view" : "desktop-view"}>
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
</div>
<div class={disableMobileView ? "no-view" : "mobile-view"}>
  <Rank scores={scores} currentPlayerId={currentPlayerId} />
</div>


<style>
  .desktop-view {
    display: block;
  }

  .mobile-view {
    display: none;
  }

  .no-view {
    display: none;
  }

  .always-view {
    display: block;
  }

  @media (max-width: 600px) {
    .desktop-view {
      display: none;
    }

    .mobile-view {
      display: block;
    }
  }
</style>


<script>
  import List, { Item, Separator, Text } from '@smui/list'; 
  import Score from "./score.svelte";
  import Rank from './rank.svelte';
  /**
   * @type {Object.<string, number>}
   */
  export let scores = {}
  export let currentPlayerId = ""
  export let disableMobileView = false
  let rank = 0
  $: scores, rank = calculateRank()

  function calculateRank() {
    let sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1])
    let rank = sortedScores.findIndex(([key, value]) => key === currentPlayerId) + 1
    return rank
  }
</script>