import { IProject, IProjectFilters, IProjectRole, IProjectInvitation, IResearcherRoleType } from "@/interfaces"
import { apiCore } from "./core"

export const apiProject = {
  // REFERENCES
  async getMulti(token: string, payload: IProjectFilters = {}) {
    return await useFetch<IProject[]>(`${apiCore.url()}/project/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: IProject) {
    return await useFetch<IProject>(`${apiCore.url()}/project`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: IProject) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addTask(token: string, key: string, task_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/task/${task_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTask(token: string, key: string, task_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/task/${task_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addSchema(token: string, key: string, schema_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/schema/${schema_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeSchema(token: string, key: string, schema_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/schema/${schema_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  // MANAGE PROJECT MEMBERS
  async getAllMembers(token: string, key: string, payload: IProjectFilters = {}) {
    return await useFetch<IProjectRole[]>(`${apiCore.url()}/project/${key}/members`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async updateMember(token: string, key: string, member_key: string, role_type: IResearcherRoleType, payload: IProjectFilters = {}) {
    return await useFetch<IProjectRole[]>(`${apiCore.url()}/project/${key}/members/${member_key}/${role_type}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async removeMember(token: string, key: string, member_key: string, payload: IProjectFilters = {}) {
    return await useFetch<IProjectRole[]>(`${apiCore.url()}/project/${key}/members/${member_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getAllInvitations(token: string, key: string, payload: IProjectFilters = {}) {
    return await useFetch<IProjectInvitation[]>(`${apiCore.url()}/project/${key}/invitations`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async createInvitation(token: string, key: string, email: string, payload: IProjectFilters = {}) {
    return await useFetch<IProjectInvitation[]>(`${apiCore.url()}/project/${key}/invitations/${email}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async removeInvitation(token: string, key: string, invitation_key: string, payload: IProjectFilters = {}) {
    return await useFetch<IProjectInvitation[]>(`${apiCore.url()}/project/${key}/invitations/${invitation_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
}