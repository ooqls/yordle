import { readable } from "svelte/store";

const context = readable({clientId: ""}, (set) => {
  const clientId = localStorage.getItem("clientId");
  if (clientId) {
    set({clientId});
  }
})