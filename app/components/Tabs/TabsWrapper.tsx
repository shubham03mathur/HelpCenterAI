import type { tabElement } from "@/app/types/commonTypes";
import { Tabs } from "@heroui/react";

interface Itabs {
  tabs: tabElement[];
}

const TabsWrapper: React.FC<Itabs> = ({ tabs }) => {
  return (
    <Tabs className="w-full max-w-6xl">
      <Tabs.ListContainer className="mx-auto w-full max-w-md">
        <Tabs.List>
          {tabs?.map((tab) => {
            return (
              <Tabs.Tab id={tab.id} key={tab.id}>
                {tab.name}
                <Tabs.Indicator />
              </Tabs.Tab>
            );
          })}
        </Tabs.List>
      </Tabs.ListContainer>
      {
        tabs?.map(tab => {
          const Component = tab.component;
          return (
            <Tabs.Panel className="pt-4" id={tab.id} key={tab.id}>
              {tab?.heroElement && tab?.heroElement() }
              <Component />
            </Tabs.Panel>
          )
        })
      }
    </Tabs>
  );
};

export default TabsWrapper;
