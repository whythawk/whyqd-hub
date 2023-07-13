<template>
  <div class="bg-white">
    <slot name="header">
      <!-- Responsive menus -->
      <NavigationDefaultSidebarMenu />
      <NavigationDefaultMobileMenu />
    </slot>
    <slot />
    <slot name="sidebar">
      <NavigationSidebarFooter />
    </slot>
    <slot name="notifications">
      <CommonNotification />
    </slot>
  </div>
</template>