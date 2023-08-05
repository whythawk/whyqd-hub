<template>
  <div class="h-full">
    <slot />
    <slot name="footer">
      <CommonNotification />
    </slot>
  </div>
</template>