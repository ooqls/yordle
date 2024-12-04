<div class="countdown">
  {#if !displayMessage}
  <h1>
    {secondsLeft}
  </h1>
  {:else}
  <h1>
    {postMessage}
  </h1>
  {/if}
</div>
<style>
  .countdown {
    font-family: 'Roboto', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>

<script>
  import { onMount } from "svelte"
  export let delay = 0
  export let postMessage = ""
  
  let displayMessage = false
  let secondsLeft = delay
  onMount(() => {
    
    let countdown = setInterval(() => {
      secondsLeft = Math.max(secondsLeft-1, 0)
      if (secondsLeft === 0) {
        displayMessage = true
        clearInterval(countdown)
      }
    }, 1000)
  })

</script>