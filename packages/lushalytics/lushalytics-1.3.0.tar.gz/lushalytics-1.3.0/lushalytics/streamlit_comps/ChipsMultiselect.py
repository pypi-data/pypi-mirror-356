import streamlit as st

def chips_multiselect(opts, label="Label", key="chips_multiselect"):
    sk = f"{key}_sel"
    if sk not in st.session_state:                         # initialize all selected
        st.session_state[sk] = set(opts)
        for o in opts:
            st.session_state[f"{key}_{o}"] = True

    st.markdown("""
    <style>
    .chip-bar{display:flex;align-items:center;height:40px;overflow-x:auto;white-space:nowrap;
    border:1px solid #e0e0e0;border-radius:4px;padding:4px 8px;background:#fff;flex:1;}
    .chip{display:inline-block;background:#fff;border:1px solid #e0e0e0;border-radius:4px;
    padding:2px 10px;margin-right:4px;font-size:12px;color:#262730;}
    button[data-testid="baseButton-popover"],.stPopoverTarget button{min-width:160px;height:32px;
    padding:4px 12px;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    flex-shrink:0;}
    .stButton>button{height:28px;padding:2px 10px;font-size:12px;border:1px solid #e0e0e0;
    border-radius:4px;background:#fafafa;}
    [data-testid="stHorizontalBlock"]{column-gap:.5rem!important;}
    [data-testid="stPopoverContent"] .stButton>button{width:100%!important;padding:4px 0!important;
    font-size:12px!important;}
    </style>
    """, unsafe_allow_html=True)
    col = st.get_option("theme.primaryColor") or "#F63366"
    st.markdown(f"""
    <style>
    .chip{{
    display:inline-block;
    background:{col};
    color:#fff;
    border:1px solid {col};
    border-radius:4px;
    padding:2px 10px;
    margin-right:4px;
    font-size:12px;
    }}
    </style>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown(f"<div style='font-size:12px;margin-bottom:4px;'>{label}</div>",
                    unsafe_allow_html=True)

        c_btn, c_bar = st.columns([3, 7], gap="small")

        with c_btn:
            with st.popover("Select", use_container_width=True):
                q = st.text_input("Search", key=f"{key}_search")
                flt = [o for o in opts if q.lower() in o.lower()]

                if st.button("All", key=f"{key}_all", use_container_width=True):
                    for o in flt:
                        st.session_state[f"{key}_{o}"] = True
                if st.button("Clear", key=f"{key}_clr", use_container_width=True):
                    for o in opts:
                        st.session_state[f"{key}_{o}"] = False

                for o in flt:
                    st.checkbox(o, key=f"{key}_{o}")

                st.session_state[sk] = {o for o in opts
                                        if st.session_state.get(f"{key}_{o}", False)}

        with c_bar:
            chips = "".join(f'<span class="chip">{o}</span>'
                            for o in st.session_state[sk])
            st.markdown(f'<div class="chip-bar">{chips}</div>', unsafe_allow_html=True)

    return list(st.session_state[sk])