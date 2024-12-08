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
  import { run } from 'svelte/legacy';

  import List, { Item, Separator, Text } from '@smui/list'; 
  import Score from "./score.svelte";
  import Rank from './rank.svelte';
  
  /**
   * @typedef {Object} Props
   * @property {Object.<string, number>} [scores]
   * @property {string} [currentPlayerId]
   * @property {boolean} [disableMobileView]
   */

  /** @type {Props} */
  let { scores = {}, currentPlayerId = "", disableMobileView = false } = $props();
  let rank = $state(0)

  function calculateRank() {
    let sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1])
    let rank = sortedScores.findIndex(([key, value]) => key === currentPlayerId) + 1
    return rank
  }
  run(() => {
    scores, rank = calculateRank()
  });
</script>