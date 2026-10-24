import TabsWrapper from "../components/Tabs/TabsWrapper";
import { tabConfig } from "../config/tabConfig";

export default function Dashboard() {
  return (
    <TabsWrapper tabs={tabConfig}/>
  );
}
