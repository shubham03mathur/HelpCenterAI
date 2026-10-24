import type { ComponentType } from "react";

export type tabElement = {
  id: string;
  name: string;
  heroElement?: () => React.ReactNode;
  component: ComponentType;
};