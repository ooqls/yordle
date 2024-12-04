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
  export let score = 0
  export let player = ""
  let previousScore = 0
  let addScore = 0
  /**
   * @type {any}
   */
  let timer = undefined
  /**
   * 
   * @param {Number} newScore
   */
  function updateScore(newScore) {
    console.log("got a new score", newScore)
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

  $: score, updateScore(score)
</script>