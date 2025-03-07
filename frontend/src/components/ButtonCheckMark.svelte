<script>
    import CheckMark from "$components/CheckMark.svelte";
    import Button from "@smui/button";
    import { onMount } from "svelte";
    import { scale } from "svelte/transition";
    import { circIn, circInOut } from "svelte/easing";

    let props = $props()
    let showCheckMark = $state(false);

    let timer;
    function toggleCheckMark() {
        showCheckMark = !showCheckMark;
        console.log("clicked:")
        if (showCheckMark) {
            timer = setTimeout(() => {
                showCheckMark = false;
            }, 1000);
        } else {
            clearTimeout(timer);
        }

        if (props.onclick) {
            props.onclick();
        }
    }

    onMount(() => {
        console.log("mounted")
        return () => {
            clearTimeout(timer);
        };
    });
</script>

<Button {...props} onclick={toggleCheckMark} style="position: relative;">
    {@render props.children?.()}
    {#if showCheckMark}
        <div style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%);">
            <iconify-icon in:scale={{ duration: 200, easing: circIn }} out:scale={{ duration: 200, easing: circInOut }} icon="mdi:check"></iconify-icon>
        </div>
    {/if}
</Button>
