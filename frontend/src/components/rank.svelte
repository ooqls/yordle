<div>
  <b>Rank: {rank}/{Object.keys(scores).length} Score: {scores[currentPlayerId]}</b>
</div>

<script>
  /**
   * @type {Object.<string, number>}
   */
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