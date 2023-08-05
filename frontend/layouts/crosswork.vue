<template>
  <div class="bg-white">
    <slot name="header">
      <!-- Responsive menus -->
      <NavigationIconOnlyMenu />
      <NavigationDefaultMobileMenu />
    </slot>
    <main class="mt-10 md:mt-0 md:pl-20">
      <slot />
    </main>
    <slot name="notifications">
      <CommonNotification />
    </slot>
  </div>
</template>