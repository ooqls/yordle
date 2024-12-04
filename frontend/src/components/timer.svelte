<div class="timer">
  Time Left: {displaySeconds}
</div>

<style>
  .timer {
    font-family: 'Roboto', sans-serif;
    font-size: large;
  }
</style>

<script>
  import { onMount } from "svelte";

  export let secondsLeft = 0
  let displaySeconds = ""
  $: displaySeconds = Math.ceil(secondsLeft).toString().padStart(4, "0");
  $: console.log("new: ", displaySeconds);
  // let interval = setInterval(() => {
  //   if (secondsLeft <= 0) {
  //     secondsLeft = 0
  //     displaySeconds = "0000"
  //     clearInterval(interval);
  //   }
    
  // }, 1000)
  
</script>