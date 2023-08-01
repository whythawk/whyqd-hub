<template>
  <div class="container min-h-screen mx-auto">
    <header class="py-8">
      <div
        class="
          max-w-7xl
          mx-auto
          px-4
          sm:px-6
          lg:px-8
          flex
          items-center
          justify-between
        "
      >
        <h1
          class="
            flex-auto
            mt-2
            text-2xl
            font-bold
            leading-7
            text-gray-900
            sm:text-3xl sm:truncate
          "
        >
          Subscription history
        </h1>
      </div>
    </header>
    <ResourcesListFilterTable
      :resource-list="projects"
      :resource-type="resourceType"
    />
  </div>
</template>

<script lang="ts">
import { Component, Getter, Vue } from "nuxt-property-decorator"

@Component({
  middleware: "authenticated",
})
export default class Projects extends Vue {
  @Getter("teams/teams") teams
  @Getter("workflow/team") team
  @Getter("workflow/projects") projects
  public resourceType: string = "project"

  async asyncData({ store }) {
    await store.dispatch("workflow/getProjects")
    if (!store.state.teams.length) await store.dispatch("teams/getTeams")
  }
}
</script>
