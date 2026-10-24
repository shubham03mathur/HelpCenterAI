import type { tabElement } from "@/app/types/commonTypes";
import QueryForm from "../components/Form/QueryForm";
import { customerSection } from "../components/Hero/Hero";

export const tabConfig: tabElement[] = [
  {
    id: "Portal",
    name: "Customer Portal",
    heroElement: customerSection,
    component: QueryForm
  },
  {
    id: "Workspace",
    name: "Admin",
    component: () => null
  }
];
