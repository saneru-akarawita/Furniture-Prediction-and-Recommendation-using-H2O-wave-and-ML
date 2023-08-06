import { createBrowserRouter } from "react-router-dom";

import FindFurniture from "./pages/findfurniture";



const router = createBrowserRouter([
  
  {
    path: "/findFurniture",
    element: <FindFurniture />,
  },


]);

export default router;
