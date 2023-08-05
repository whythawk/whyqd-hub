<template>
  <div class="bg-white">
    <slot name="header">
      <!-- Responsive menus -->
      <NavigationDefaultSidebarMenu />
      <NavigationDefaultMobileMenu />
    </slot>
    <main class="mt-10 md:mt-0 md:pl-20 lg:pl-60 xl:pl-72">
      <div class="md:pr-52 lg:pr-72">
        <slot />
      </div>
    </main>
    <slot name="sidebar">
      <NavigationSidebarFooter />
    </slot>
    <slot name="notifications">
      <CommonNotification />
    </slot>
  </div>
</template>
