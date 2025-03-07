<script>
    import { onMount } from "svelte";

    onMount(() => {
        console.log("mounted");
        setTimeout(() => {
            this.$destroy()
        }, 1000);
    });

</script>

<iconify-icon icon="mdi:check" ></iconify-icon>