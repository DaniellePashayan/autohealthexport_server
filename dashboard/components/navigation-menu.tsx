import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import ModeToggle from "./theme-toggle";

const NavbarMenu = () => {
    return (
        <section className="py-4">
            <div className="container mx-auto flex max-w-7xl px-4 sm:px-6 lg:px-8">
                <nav className="flex items-center justify-between w-full">
                    {/* Centered menu items */}
                    <NavigationMenu className="flex-1 flex justify-center">
                        <NavigationMenuList className="flex space-x-4">
                            <NavigationMenuItem>
                                <NavigationMenuLink
                                    href="#"
                                    className={navigationMenuTriggerStyle()}
                                >
                                    Body Composition
                                </NavigationMenuLink>
                            </NavigationMenuItem>
                            <NavigationMenuItem>
                                <NavigationMenuLink
                                    href="#"
                                    className={navigationMenuTriggerStyle()}
                                >
                                    Activity
                                </NavigationMenuLink>
                            </NavigationMenuItem>
                            <NavigationMenuItem>
                                <NavigationMenuLink
                                    href="#"
                                    className={navigationMenuTriggerStyle()}
                                >
                                    Nutrition
                                </NavigationMenuLink>
                            </NavigationMenuItem>
                        </NavigationMenuList>
                    </NavigationMenu>
                    {/* Right-aligned theme toggle */}
                    <div className="flex items-center justify-end flex-none ml-4">
                        <ModeToggle />
                    </div>
                </nav>
            </div>
        </section>
    );
};

export { NavbarMenu };
