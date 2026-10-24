import { Card as CardWrapper } from "@heroui/react";
import type { CardVariants } from "@heroui/react";
import type { ComponentType } from "react";


interface ICard {
  variant?: CardVariants["variant"];
  title: string;
  description: React.ReactNode;
  footer?: React.ReactNode;
  content: ComponentType;
}

const CustomerQueryCard: React.FC<ICard> = ({
  title,
  description,
  content: Component,
  footer,
  variant = "transparent",
}) => (
  <CardWrapper variant={variant} className="w-full max-w-md">
    <CardWrapper.Header>
      <CardWrapper.Title>{title}</CardWrapper.Title>
      <CardWrapper.Description>{description}</CardWrapper.Description>
    </CardWrapper.Header>
    <CardWrapper.Content>
      <Component />
    </CardWrapper.Content>
    <CardWrapper.Footer>{footer}</CardWrapper.Footer>
  </CardWrapper>
);

export default CustomerQueryCard;
