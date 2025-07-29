use nadi_plugin::nadi_internal_plugin;

#[nadi_internal_plugin]
mod attributes {
    use crate::prelude::*;
    use abi_stable::std_types::Tuple2;
    use nadi_plugin::{env_func, network_func, node_func};
    use std::str::FromStr;
    use string_template_plus::Template;

    /// Set node attributes
    ///
    /// Use this function to set the node attributes of all nodes, or
    /// a select few nodes using the node selection methods (path or
    /// list of nodes)
    ///
    /// # Error
    /// The function should not error.
    ///
    /// # Example
    /// Following will set the attribute `a2d` to `true` for all nodes
    /// from `A` to `D`
    ///
    /// ```task
    /// node[A -> D] set_attrs(a2d = true)
    /// ```
    #[node_func]
    fn set_attrs(
        node: &mut NodeInner,
        /// Key value pairs of the attributes to set
        #[kwargs]
        attrs: &AttrMap,
    ) -> Result<(), String> {
        for Tuple2(k, v) in attrs {
            node.set_attr(k.as_str(), v.clone());
        }
        Ok(())
    }

    /// Retrive attribute
    #[node_func]
    fn get_attr(
        node: &NodeInner,
        /// Name of the attribute to get
        attr: &str,
        /// Default value if the attribute is not found
        default: Option<Attribute>,
    ) -> Option<Attribute> {
        node.attr(attr).cloned().or(default)
    }

    /// Check if the attribute is present
    #[node_func]
    fn has_attr(
        node: &NodeInner,
        /// Name of the attribute to check
        attr: &str,
    ) -> bool {
        node.attr(attr).is_some()
    }

    /// Return the first Attribute that exists
    #[node_func]
    fn first_attr(
        node: &NodeInner,
        /// attribute names
        attrs: &[String],
        /// Default value if not found
        default: Option<Attribute>,
    ) -> Option<Attribute> {
        for attr in attrs {
            if let Ok(Some(v)) = node.attr_dot(attr) {
                return Some(v.clone());
            }
        }
        default
    }

    /// map values from the attribute based on the given table
    #[env_func]
    fn strmap(
        /// Value to transform the attribute
        #[relaxed]
        attr: &str,
        /// Dictionary of key=value to map the data to
        attrmap: &AttrMap,
        /// Default value if key not found in `attrmap`
        default: Option<Attribute>,
    ) -> Option<Attribute> {
        attrmap.get(attr).cloned().or(default)
    }

    /// if else condition with multiple attributes
    #[node_func]
    fn set_attrs_ifelse(
        node: &mut NodeInner,
        /// Condition to check
        #[relaxed]
        cond: bool,
        /// key = [val1, val2] where key is set as first if `cond` is true else second
        #[kwargs]
        values: &AttrMap,
    ) -> Result<(), String> {
        for Tuple2(k, v) in values {
            let (t, f) = FromAttribute::try_from_attr(v)?;
            let v = if cond { t } else { f };
            node.set_attr(k, v);
        }
        Ok(())
    }

    /// Set node attributes based on string templates
    #[node_func]
    fn set_attrs_render(
        node: &mut NodeInner,
        /// key value pair of attribute to set and the Template to render
        #[kwargs]
        kwargs: &AttrMap,
    ) -> Result<(), String> {
        for Tuple2(k, v) in kwargs {
            let templ: Template = Template::try_from_attr(v)?;
            let text = node.render(&templ).map_err(|e| e.to_string())?;
            node.set_attr(k.as_str(), text.into());
        }
        Ok(())
    }

    /// Set node attributes based on string templates
    #[node_func(echo = false)]
    fn load_toml_render(
        node: &mut NodeInner,
        /// String template to render and load as TOML string
        toml: &Template,
        /// Print the rendered toml or not
        echo: bool,
    ) -> anyhow::Result<()> {
        let toml = format!("{}\n", node.render(toml)?);
        if echo {
            println!("{toml}");
        }
        let tokens = crate::parser::tokenizer::get_tokens(&toml);
        let attrs = crate::parser::attrs::parse(tokens)?;
        node.attr_map_mut().extend(attrs);
        Ok(())
    }

    /// Set node attributes based on string templates
    #[env_func]
    fn parse_attr(
        /// String to parse into attribute
        toml: &str,
    ) -> Result<Attribute, String> {
        Attribute::from_str(toml).map_err(|e| e.to_string())
    }

    /// Set node attributes based on string templates
    #[env_func]
    fn parse_attrmap(
        /// String to parse into attribute
        toml: String,
    ) -> Result<AttrMap, String> {
        let tokens = crate::parser::tokenizer::get_tokens(&toml);
        let attrs = crate::parser::attrs::parse(tokens).map_err(|e| e.to_string())?;
        Ok(attrs)
    }

    /// get the choosen attribute from Array or AttrMap
    #[env_func]
    fn get(parent: Attribute, index: Attribute) -> Result<Attribute, String> {
        match (parent, index) {
            (Attribute::Array(ar), Attribute::Integer(ind)) => ar
                .get(ind as usize)
                .cloned()
                .ok_or(format!("Index {ind} not found")),
            (Attribute::Table(am), Attribute::String(key)) => am
                .get(&key)
                .cloned()
                .ok_or(format!("Index {key} not found")),
            (Attribute::Array(_), b) => Err(format!(
                "Array index should be Integer not {}",
                b.type_name()
            )),
            (Attribute::Table(_), b) => Err(format!(
                "AttrMap index should be String not {}",
                b.type_name()
            )),
            (a, _) => Err(format!("{} cannot be indexed", a.type_name())),
        }
    }

    /// map values from the attribute based on the given table
    #[env_func]
    fn float_transform(
        /// value to transform
        #[relaxed]
        value: f64,
        /// transformation function, can be one of log/log10/sqrt
        transformation: &str,
    ) -> Result<Attribute, String> {
        let value = if value == 0.0 { value + 0.1 } else { value };
        // let attr = String::from_attr_relaxed(node.attr(attr)?)?;
        Ok(Attribute::Float(match transformation {
            "log" => value.ln(),
            "log10" => value.log10(),
            "sqrt" => value.sqrt(),
            t => return Err(format!("Unknown Transformation: {t}")),
        }))
    }

    /// map values from the attribute based on the given table
    #[env_func]
    fn float_div(
        /// numerator
        #[relaxed]
        value1: f64,
        /// denominator
        #[relaxed]
        value2: f64,
    ) -> f64 {
        value1 / value2
    }

    /// map values from the attribute based on the given table
    #[env_func]
    fn float_mult(
        /// numerator
        #[relaxed]
        value1: f64,
        /// denominator
        #[relaxed]
        value2: f64,
    ) -> f64 {
        value1 * value2
    }

    /// Set network attributes
    ///
    /// # Arguments
    /// - `key=value` - Kwargs of attr = value
    #[network_func]
    fn set_attrs(
        network: &mut Network,
        /// key value pair of attributes to set
        #[kwargs]
        attrs: &AttrMap,
    ) -> Result<(), String> {
        for Tuple2(k, v) in attrs {
            network.set_attr(k.as_str(), v.clone());
        }
        Ok(())
    }

    /// Set network attributes based on string templates
    #[network_func]
    fn set_attrs_render(
        network: &mut Network,
        /// Kwargs of attr = String template to render
        #[kwargs]
        kwargs: &AttrMap,
    ) -> Result<(), String> {
        for Tuple2(k, v) in kwargs {
            let templ: Template = Template::try_from_attr(v)?;
            let text = network.render(&templ).map_err(|e| e.to_string())?;
            network.set_attr(k.as_str(), text.into());
        }
        Ok(())
    }
}
