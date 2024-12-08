<div class="rank-container">
  <b>Rank: {rank}/{Object.keys(scores).length}</b> 
  <b>Score: {scores[currentPlayerId]}</b>
</div>

<style>
  .rank-container {
    display: flex;
    flex-direction: column;
    font-size: large;
  }
</style>

<script>
  import { run } from 'svelte/legacy';

  
  /**
   * @typedef {Object} Props
   * @property {Object.<string, number>} [scores]
   * @property {string} [currentPlayerId]
   */

  /** @type {Props} */
  let { scores = {}, currentPlayerId = "" } = $props();
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