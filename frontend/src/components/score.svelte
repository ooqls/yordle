<div class="score-entry">
  <strong>{player}: </strong>
  { previousScore }
  {#if addScore > 0}
  + { addScore }
{/if}
</div>

<style>
.score-entry {
  font-size: larger;
}
</style>

<script>
    import { onMount } from "svelte";


  /**
   * @typedef {Object} Props
   * @property {number} [score]
   * @property {string} [player]
   */

  /** @type {Props} */
  let { score = 0, player = "" } = $props();
  let previousScore = $state(0)
  let addScore = $state(0)
  /**
   * @type {any}
   */
  let timer = undefined


  onMount(() => {
    timer = setInterval(() => {
      if (addScore > 0) {
        let addup = setInterval(() => {
          if (addScore > 0) {
            addScore -= 1
            previousScore += 1
          } else {
            clearInterval(addup)
          }
        }, 10)
      }

    }, 2000)

    return () => { clearInterval(timer) }
  })
  /**
   * 
   * @param {Number} newScore
   */
  function updateScore(newScore) {
    console.log("updating score")
    if (newScore == previousScore) {
      return
    }

    addScore = newScore - previousScore

  }


  $effect(() => updateScore(score))

</script>