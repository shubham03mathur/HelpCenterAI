"use client";
import { useActionState } from "react";
import { handleQueryFormAction } from "@/app/actions/action";
import { Check } from "@gravity-ui/icons";
import {
  Button,
  FieldError,
  Form,
  Input,
  Label,
  TextField,
  TextArea,
  Card,
} from "@heroui/react";


const QueryForm = () => {
  const [state, formAction, isPending] = useActionState(handleQueryFormAction, null);

  return (
    <div className="grid w-full md:grid-cols-1 gap-4 lg:grid-cols-2">
      <Card className="w-full max-w-md bg-surface text-foreground border border-border p-10">
        <Card.Header>
          <Card.Title className="text-2xl mb-2.5">Start a Conversation!</Card.Title>
          <Card.Description>
            Our assistant will look for an answer first and bring in a
            specialist when needed.
          </Card.Description>
        </Card.Header>
        <Form className="flex w-full max-w-96 flex-col gap-4" action={formAction}>
          <TextField
            className="text-foreground"
            isRequired
            name="email"
            type="email"
            validate={(value) => {
              if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value)) {
                return "Please enter a valid email address";
              }
              return null;
            }}
          >
            <Label className="text-foreground">Email</Label>
            <Input placeholder="john@example.com" />
            <FieldError />
          </TextField>
          <TextField
            className="text-foreground"
            isRequired
            name="help"
            type="text"
            validate={(value) => {
              if (!value) {
                return "Please enter the topic you need help with.";
              }
              return null;
            }}
          >
            <Label className="text-foreground">
              What do you need help with?
            </Label>
            <Input placeholder="e.g. Billing support" />
            <FieldError />
          </TextField>
          <TextField
            className="text-foreground"
            isRequired
            name="details"
            type="text"
            validate={(value) => {
              if (!value) {
                return "Please elobrate your concern.";
              }
              return null;
            }}
          >
            <Label className="text-foreground">Tell us more</Label>
            <TextArea
              aria-label="explain your concern"
              id="textarea-rows-6"
              placeholder="Include any details that might help..."
              rows={6}
              style={{ resize: "vertical" }}
            />
            <FieldError />
          </TextField>

          <div className="flex gap-2">
            <Button type="submit" isPending={isPending}>
              <Check />
              { isPending ? 'Sending...' : 'SUBMIT'}
            </Button>
            <Button type="reset" variant="secondary">
              Reset
            </Button>
          </div>
        </Form>
      </Card>
      <Card className="w-full max-w-md bg-surface text-foreground border border-border p-10">
        <Card.Header>
          <Card.Title className="text-2xl mb-2.5">Popular topics</Card.Title>
          <Card.Description>
            Quick answers to common questions.
          </Card.Description>
        </Card.Header>
        <Card.Content>
          <div className="flex flex-col divide-y divide-border">
            <div className="flex flex-col gap-2 p-2">
              <div className="text-sm">Reset your password</div>
              <div className="text-muted-foreground text-xs">Account access • 2 mins read</div>
            </div>
            <div className="flex flex-col gap-2 p-2">
              <div className="text-sm">Export reports as PDF</div>
              <div className="text-muted-foreground text-xs">Reports • 4 mins read</div>
            </div>
            <div className="flex flex-col gap-2 p-2">
              <div className="text-sm">Manage subscription billing</div>
              <div className="text-muted-foreground text-xs">Billing • 5 mins read</div>
            </div>
            <div className="flex flex-col gap-2 p-2">
              <div className="text-sm">API integration guide</div>
              <div className="text-muted-foreground text-xs">Developers • 5 mins read</div>
            </div>
          </div>
        </Card.Content>
      </Card>
    </div>
  );
};

export default QueryForm;
