import { createContext } from "react"

export const FunctionDialogContext = createContext({
    analysis_state: null,
    analysis_setter: null,
    query_state: null,
    query_setter: null
});

const NavBarContext = createContext({
    tab_setter: null
});

export {NavBarContext};
