// types/User.ts
export interface User {
    id: number;
    username: string;
    email: string;
    role: Role;
  }
  
  // types/Role.ts
  export type Role = 'Author' | 'Collaborator';
  
  // types/Section.ts
  export interface Section {
    id: number;
    title: string;
    content: string;
    parentSectionId: number | null;
    childSections: Section[];
  }