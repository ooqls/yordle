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
  import { run } from 'svelte/legacy';

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
  /**
   * 
   * @param {Number} newScore
   */
  function updateScore(newScore) {
    let newAddScore = newScore - previousScore
    if (timer !== undefined) {
      clearTimeout(timer)
    }

    addScore = newAddScore
    timer = setTimeout(()=>{
      let diff = Math.max(Math.ceil(addScore / 100), 1)
      let addUp = setInterval(() => {
        previousScore += diff
        addScore -= diff
        if (addScore <=  0) {
          clearInterval(addUp)
        }
      }, 1)
    }, 2000)


  }


  $effect(() => updateScore(score))

</script>